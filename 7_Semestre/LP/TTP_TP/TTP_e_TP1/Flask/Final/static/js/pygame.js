
const chessBoard = document.getElementById('chess-board');
const chessContainer = document.getElementById('chess-container');

chessContainer.addEventListener('click', (event) => {
    const rect = chessContainer.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    fetch(`/chess_move?x=${x}&y=${y}`)
        .then(response => response.json())
        .then(data => {
            if (data.board_image) {
                chessBoard.src = 'data:image/png;base64,' + data.board_image;
            }
        });
});
 