var canvas = document.querySelector('canvas[jsname="UzWXSb"]');
var context = canvas.getContext("2d");


// Set the number of rows and columns in the game board
var numRows = 15;
var numCols = 17;

function drawGrid() {
  // Get the pixel data for the entire canvas
  var imageData = context.getImageData(0, 0, canvas.width, canvas.height);
  var pixelData = imageData.data;

  // Determine the size of each cell in pixels
  var cellWidth = (canvas.width - 56) / numCols;
  var cellHeight = (canvas.height - 50) / numRows;

  var grid = [];
  // Loop through each cell in the game board
  for (var row = 0; row < numRows; row++) {
    var rowArray = [];
    for (var col = 0; col < numCols; col++) {
      // Determine the pixel coordinates of the top-left corner of the cell
      var x = col * cellWidth;
      var y = row * cellHeight;

      // Get the pixel data for the current cell
      var imageData = context.getImageData(
        x + 28,
        y + 25,
        cellWidth,
        cellHeight
      );
      var pixelData = imageData.data;

      // Count the number of pixels for each color
      var colorCounts = { R: 0, G: 0, B: 0, W: 0, Mouth: 0 };
      for (var i = 0; i < pixelData.length; i += 4) {
        var R = pixelData[i];
        var G = pixelData[i + 1];
        var B = pixelData[i + 2];
        if (R === 255 && G === 255 && B === 255) {
          colorCounts.W++;
        } else if (R > G && R > B) {
          colorCounts.R++;
        } else if (G > R && G > B) {
          colorCounts.G++;
        } else if (R === 28 && G === 70 && B === 157) {
          colorCounts.Mouth++;
        } else {
          colorCounts.B++;
        }
      }

      // Determine the dominant color for the current cell
      var dominantColor;
      if (colorCounts.W >= 40) {
        dominantColor = "H";
        context.fillStyle = "yellow";
      } else if (
        colorCounts.R > colorCounts.G &&
        colorCounts.R > colorCounts.B
      ) {
        dominantColor = "R";
        context.fillStyle = "red";
      } else if (
        colorCounts.G > colorCounts.R &&
        colorCounts.G > colorCounts.B * 2
      ) {
        dominantColor = "G";
        context.fillStyle = "green";
      } else if (colorCounts.Mouth >= 50) {
        dominantColor = "G";
        context.fillStyle = "green";
      } else {
        dominantColor = "B";
        context.fillStyle = "blue";
      }

      // Fill the cell with the dominant color
      context.fillRect(x + 28, y + 25, cellWidth, cellHeight);

      // Draw a rectangle around the cell
      context.strokeRect(x + 28, y + 25, cellWidth, cellHeight);

      // Write the first letter of the dominant color in the center of the cell
      context.font = "16px Arial";
      context.fillStyle = "#000";
      context.textAlign = "center";
      context.fillText(
        dominantColor,
        x + cellWidth / 2 + 28,
        y + cellHeight / 2 + 25
      );

      rowArray.push(dominantColor);
    }
    grid.push(rowArray);
  }
  // console.log(getNextMove(grid));
  // 
  
  (getNextMove(grid));
}