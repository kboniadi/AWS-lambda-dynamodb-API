$(document).ready(function () {
  $(".editbtn").on("click", function () {
    $("#editmodal").modal("show");
    let $tr = $(this).closest("tr");
    let data = $tr
      .children("td")
      .map(function () {
        return $(this).text();
      })
      .get();

    let Imagedata = [];
    Imagedata.push($tr.find("img").attr("src"));

    $("#SetImage").attr("src", Imagedata[0]);
    $("#title").val(data[0]);
    $("#quantity").val(data[1]);
    $("#size").val(data[2]);
  });
});
