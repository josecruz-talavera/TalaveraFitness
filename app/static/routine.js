// JavaScript to handle video link clicks
document.querySelectorAll('.video-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();  // Prevent the default link behavior
        const videoUrl = this.getAttribute('data-video-url');  // Get the video URL from the data attribute
        // Redirect to the play page with the video URL as a query parameter
        window.location.href = `/play?video_url=${encodeURIComponent(videoUrl)}`;
    });
});