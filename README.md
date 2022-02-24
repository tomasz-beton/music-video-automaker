# Music video automaker
Have you ever watched muted commercials with music playing in the background? Well, maybe not. 
Anyways I can assure you it sound/looks very cool when cuts in the video synchronize with the beat.

That was our general idea. If we detect cuts in provided video, detect beat in a provided soundtrack, we can create something along the lines of a music video.

#### Usage: 
`
python merge_testing.py <video_path> <audio_path> [options]
`

You can specify output file path using `-o <out_path>` and other options which you better look up yourself in the code.

example: 
`
python merge_testing.py "src/penguins.mp4" "src/blinding_lights.mp3" -o "out/merged.mp4" --threshold 2
`
