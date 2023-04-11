var app = angular.module('chromeTabsApp', ['ui.bootstrap']);
app
  .controller('AppCtrl', ['$scope', function ($scope) {
    var counter = 1;
    $scope.tabs = [];

    var addTab = function () {
      $scope.tabs.push({ title: 'Tab ' + counter, content: 'Tab ' + counter });
      counter++;
      $scope.tabs[$scope.tabs.length - 1].active = true;
    };

    var removeTab = function (event, index) {
      event.preventDefault();
      event.stopPropagation();
      $scope.tabs.splice(index, 1);
    };

    $scope.addTab    = addTab;
    $scope.removeTab = removeTab;

    for (var i = 0; i < 5; i++) {
      addTab();
    }
  }])
  .directive('tabHighlight', [function(){
    return {
      restrict: 'A',
      link: function(scope, element) {
        var x, y, initial_background = '#c3d5e6';

        element
          .removeAttr('style')
          .mousemove(function (e) {
            // Add highlight effect on inactive tabs
            if(!element.hasClass('active'))
            {
              x = e.pageX - this.offsetLeft;
              y = e.pageY - this.offsetTop;

              element
                .css({ background: '-moz-radial-gradient(circle at ' + x + 'px ' + y + 'px, rgba(255,255,255,0.4) 0px, rgba(255,255,255,0.0) 45px), ' + initial_background })
                .css({ background: '-webkit-radial-gradient(circle at ' + x + 'px ' + y + 'px, rgba(255,255,255,0.4) 0px, rgba(255,255,255,0.0) 45px), ' + initial_background })
                .css({ background: 'radial-gradient(circle at ' + x + 'px ' + y + 'px, rgba(255,255,255,0.4) 0px, rgba(255,255,255,0.0) 45px), ' + initial_background });
            }
          })
          .mouseout(function () {
            element.removeAttr('style');
          });
      }
    };
  }]);
