from app import db, jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import redis
import rq
from pydantic import Field
from pydantic import BaseModel



@jwt.user_lookup_loader
def user_loader_callback(jwt_header: dict, jwt_data: dict) -> object:
    """
    HUser loader function which uses the JWT identity to retrieve a user object. Method is called on protected routes

    Parameters
    ----------
    jwt_header : dictionary
        header data of the JWT
    jwt_data : dictionary
        payload data of the JWT

    Returns
    -------
    object
        Returns a users object containing the user information
    """
    return Users.query.filter_by(id=jwt_data["sub"]).first()


# defines the Users database table
class Users(BaseModel):
    email: str = Field(..., example='example@cfgi.com')
    password_hash: str = Field(..., example='password')

    def set_password(self, password: str):
        """
        Helper function to generate the password hash of a user

        Parameters
        ----------
        password : str
            The password provided by the user when registering
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Helper function to verify the password hash agains the password provided by the user when logging in

        Parameters
        ----------
        password : str
            The password provided by the user when logging in

        Returns
        -------
        bool
            Returns True if the password is a match. If not False is returned
        """
        return check_password_hash(self.password_hash, password)

    def launch_task(self, name: str, description: str, **kwargs) -> object:
        """
        Helper function to launch a background task

        Parameters
        ----------
        name : str
            Name of the task to launch
        description : str
            Description of the task to launch

        Returns
        -------
        object
            A Tasks object containing the task information
        """
        rq_job = current_app.task_queue.enqueue(
            "app.tasks.long_running_jobs" + name, **kwargs
        )
        task = Tasks(
            task_id=rq_job.get_id(), name=name, description=description, user=self
        )
        db.session.add(task)

        return task

    def get_tasks_in_progress(self) -> list:
        """
        Helper function which retrieves the background tasks that are still in progress

        Returns
        -------
        list
            A list of Tasks objects
        """
        return Tasks.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name: str) -> object:
        """
        Helper function to retrieve a task in progress based on name

        Parameters
        ----------
        name : str
            name of the task to be retrieved

        Returns
        -------
        object
            A task object
        """
        return Tasks.query.filter_by(name=name, user=self, complete=False).first()

    def get_completed_tasks(self) -> dict:
        """
        Helper function to retrieve all completed tasks

        Returns
        -------
        dict
            A dictionary of Tasks objects
        """
        return Tasks.query.filter_by(user=self, complete=True).all()



class Tasks(BaseModel):
    id: int = Field(..., example='number')
    task_id: str = Field(..., example='index')
    name: str = Field(..., example='name')
    description: str = Field(..., example='description')
    user_id: str = Field(..., example='user email')
    complete: bool = Field(..., example='completed')

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.task_id, connection=current_app.redis)

        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None

        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get("progress", 0) if job is not None else 100
