ffmpeg_subtitle_scene_extraction
================================
This tools takes a movie file and a subtitles file and prints ffmpeg commands
that will chop the entire movie up into clips, one clip for each span of time
that a subtitle appears on the screen. It also produces commands that will
extract clips for all durations when no subtitles are shown on the screen.

Note that this program does not actually execute any ffmpeg commands, it only
prints commands that should be executed. This makes it easier to verify that
the commands are sane before any expensive extraction operations are executed.

File Input/Output
=================
This program should be executed as follows:

python subtitles.py [movie_file] [subtitle_file]

It will print a series of ffmpeg commands that will extract each clip.

ffmpeg -ss 00:00:00.000 -i "2012 Moonrise Kingdom.mp4" -t 00:01:30.376 -sameq -async 1 lines/000000_zzz.mp4
ffmpeg -ss 00:01:30.376 -i "2012 Moonrise Kingdom.mp4" -t 00:00:01.250 -sameq -async 1 lines/000001_in_order_to_show_you_how.mp4
ffmpeg -ss 00:01:31.626 -i "2012 Moonrise Kingdom.mp4" -t 00:00:00.083 -sameq -async 1 lines/000001_zzz.mp4
ffmpeg -ss 00:01:31.709 -i "2012 Moonrise Kingdom.mp4" -t 00:00:02.500 -sameq -async 1 lines/000002_a_big_symphonyorchestra_is_put_together.mp4
ffmpeg -ss 00:01:34.209 -i "2012 Moonrise Kingdom.mp4" -t 00:00:00.083 -sameq -async 1 lines/000002_zzz.mp4

If you want execute the commands you should redirect the output to a file
and execute it:

python subtitles.py [movie_file] [subtitle_file] > extract.sh
chmod +x extract.sh
./extract.sh

Note that the commands alternate between extracting a clip that has a subtitle
and a clip that has no subtitle. This ensures that the entire movie is broken
into clips, whether that portion of the movie was showing a subtitle or not.
The clips without subtitles are usually longer scenic sequenes without dialogue.

Clips with subtitles will include the sequence number of the subtitle and the
subtitle text in their filename.

Clips without subtitles will have a seuqnce number equal to one less than the subtitle
appearing after them and will all be named "zzz," as if the actors are taking naps
between dialogue.

SubRip Format
===============
This program expects the subtitle file to be in the SubRup format. What follows
is my own explanation of the file format, but a more exact definition may be found
on the [SubRip wikipedia article](http://en.wikipedia.org/wiki/SubRip).

Here is an example of an actual subtitle entry:

1
00:01:30,376 --> 00:01:31,626
Hello World.
Welcome to my movie.

Here are the abstract components of the entry:

[subtitle_sequence_number]
[timestamp_start] --> [timestamp_end]
Subtitle text
Possible spanning multiple lines.
[a blank line]

The subtitle_sequence_number should be an int and is used to keep the extracted
scenes in order. The timestamp_start and timestamp_end represent when the subtitle
should appear on the screen and when it should disappear. These time are seperated
by the --> symbol.

Each timestamp is of the form:

[hour]:[minute]:[second],[millisecond]

Here is a sample of actual subtitles for the beginning of Moonrise Kingdom:

1
00:01:30,376 --> 00:01:31,626
In order to show you how

2
00:01:31,709 --> 00:01:34,209
a big symphony
orchestra is put together,

3
00:01:34,292 --> 00:01:37,376
Benjamin Britten
has written a big piece of music,

4
00:01:37,459 --> 00:01:39,209
which is made up
of smaller pieces

5
00:01:39,292 --> 00:01:42,292
that show you all
the separate parts of the orchestra.

6
00:01:42,376 --> 00:01:45,167
These smaller pieces
are called variations,

7
00:01:45,251 --> 00:01:48,751
which means different ways
of playing the same tune.

8
00:01:48,876 --> 00:01:52,084
First of all,
he lets us hear the tune or the theme,

9
00:01:52,167 --> 00:01:53,292
which is a beautiful melody

10
00:01:53,376 --> 00:01:56,751
by the much older
British composer Henry Purcell.
