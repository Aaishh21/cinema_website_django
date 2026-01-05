const playButton = document.getElementById('playButton');
const filmVideo = document.getElementById('filmVideo');
const thumbnail = document.getElementById('thumbnail');

playButton.addEventListener('click', () => {
  playButton.style.display = 'none';
  thumbnail.style.opacity = '0';
  filmVideo.style.display = 'block';
  filmVideo.play();
});

filmVideo.addEventListener('ended', () => {
  filmVideo.style.display = 'none';
  thumbnail.style.opacity = '1';
  playButton.style.display = 'flex';
});