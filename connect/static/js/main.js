  $("#login-form").submit(function(e) {
    e.preventDefault();

    // Get the values from the form
    var ip_address = $("#ip_address").val();
    var username = $("#username").val();
    var password = $("#password").val();

    // Validate the login info
    if (ip_address !== "" && username !== "" && password !== "") {
      // Send an AJAX request to the login view
      $.ajax({
        url: "/login/",
        type: "POST",
        data: {
          ip_address: $("#ip_address").val(),
          username: $("#username").val(),
          password: $("#password").val(),
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data) {
          if (data.result === "success") {
            alert(data.message);

            // Create the new tab and add it to the tabs list
            var new_tab_title = $("#ip_address").val();
            var new_tab = '<li class="nav-item"><a class="nav-link" id="' + new_tab_title + '-tab" data-toggle="tab" href="#' + new_tab_title + '" role="tab" aria-controls="' + new_tab_title + '" aria-selected="false">' + new_tab_title + '</a><span class="ui-icon ui-icon-close" role="presentation">Remove Tab</span></li>';
            $('#myTab').append(new_tab);

            // Add the content for the new tab
            var new_tab_content = '<div class="tab-pane fade" id="' + new_tab_title + '" role="tabpanel" aria-labelledby="' + new_tab_title + '-tab"><p>Content for tab ' + new_tab_title + '</p></div>';
            $('#myTabContent').append(new_tab_content);

            // Close the modal and reset the form
            $("#addDeviceModal").modal("hide");
            $("#add-device-form")[0].reset();

            // Redirect to arista_data with new device query parameter
            window.location.href = '/arista_data/?new_device=' + new_tab_title;
          } else {
            alert(data.message);
          }
        },
        error: function(xhr, status, error) {
          alert("An error occurred while trying to connect to the device.");
        }
      });
    } else {
      alert("Please provide all the login information.");
    }
  });

  $(document).ready(function() {
    $('#myTab a').on('click', function(e) {
      e.preventDefault();
      $(this).tab('show');
    });

    $("#add-tab-btn").click(function() {
      $("#addDeviceModal").modal();
    });

    var tabs = $("#myTab").tabs({
      activate: function(event, ui) {
        if (ui.newTab.is("#add-tab")) {
          $("#addDeviceModal").modal();
          tabs.tabs('select', -2);
        }
      }
    });

    // Close icon: removing the tab on click
    tabs.delegate("span.ui-icon-close", "click", function() {
      var panelId = $(this).closest("li").remove().attr("aria-controls");
      $("#" + panelId).remove();
      tabs.tabs("refresh");
    });
  });