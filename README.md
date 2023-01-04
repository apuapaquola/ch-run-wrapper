# ch-run-wrapper

## Wraper for ch-run to use squashfs charliecloud images.


Current charliecloud implementation of ch-run is not working with squashfs container images. As a workaround, ch-run-wrapper will:

* mount a container image with squashfuse
* call ch-run on the mounted image
* unmount the image

