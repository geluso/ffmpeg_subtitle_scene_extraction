#!/opt/local/bin/python2.7

import argparse
import codecs
import collections
import re

Timestamp = collections.namedtuple("Timestamp", "hour minute second millisecond")

def parse_timestamp(timestamps):
  start, end = timestamps.split(" --> ")
  start = parse_single_timestamp(start)
  end = parse_single_timestamp(end)
  return start, end

def parse_single_timestamp(timestamp):
  hour, minute, second = timestamp.split(":")
  second, millisecond = second.split(",")
  return Timestamp(int(hour), int(minute), int(second), int(millisecond))

MILLISECOND_PER_SECOND = 1000
MILLISECOND_PER_MINUTE = MILLISECOND_PER_SECOND * 60
MILLISECOND_PER_HOUR = MILLISECOND_PER_MINUTE * 60

def timestamp_to_millisecond(timestamp):
  total = timestamp.millisecond
  total += timestamp.second * MILLISECOND_PER_SECOND
  total += timestamp.minute * MILLISECOND_PER_MINUTE
  total += timestamp.hour * MILLISECOND_PER_HOUR
  return total

def millisecond_to_timestamp(millisecond):
  hour = millisecond / MILLISECOND_PER_HOUR
  millisecond = millisecond % MILLISECOND_PER_HOUR
  minute = millisecond / MILLISECOND_PER_MINUTE
  millisecond = millisecond % MILLISECOND_PER_MINUTE
  second = millisecond / MILLISECOND_PER_SECOND
  millisecond = millisecond % MILLISECOND_PER_SECOND
  return Timestamp(hour, minute, second, millisecond)

def timestamp_to_str(timestamp):
  return "%02d:%02d:%02d.%03d" % (timestamp.hour,
                              timestamp.minute,
                              timestamp.second,
                              timestamp.millisecond)

def parse_subtitle(movie, line_number, start, end, subtitle):
  subtitle = re.sub(" ", "_", subtitle)
  subtitle = re.sub("\s", "", subtitle)
  subtitle = re.sub("[\',\.\!\?]", "", subtitle)
  subtitle = re.sub("\<\\/?i\>", "", subtitle)
  subtitle = re.sub("\"", "'", subtitle)
  subtitle = subtitle.lower()

  output_filename = create_output_filename(line_number, subtitle)
  make_video_clip_command(movie, output_filename, start, end)

def create_output_filename(line_number, subtitle="zzz"):
  return "lines/%06d_%s.mp4" % (line_number, subtitle)

def calculate_duration(start, end):
  start_in_millisecond = timestamp_to_millisecond(start)
  end_in_millisecond = timestamp_to_millisecond(end)
  duration = end_in_millisecond - start_in_millisecond
  duration = millisecond_to_timestamp(duration)
  return duration

def make_video_clip_command(input_filename, output_filename, start, end=None):
  if end:
    duration = calculate_duration(start, end)
    duration = timestamp_to_str(duration)
    start = timestamp_to_str(start)
    print "ffmpeg -ss %s -i \"%s\" -t %s -sameq -async 1 %s" % (start, input_filename, duration, output_filename)
  else:
    start = timestamp_to_str(start)
    print "ffmpeg -ss %s -i \"%s\" -sameq -async 1 %s" % (start, input_filename, output_filename)

def parse_silence(movie, line_number, start, end=None):
  output_filename = create_output_filename(line_number)
  make_video_clip_command(movie, output_filename, start, end)

def parse_subtitles(movie, subtitles):
  previous_end = Timestamp(hour=0, minute=0, second=0, millisecond=0)
  
  while True:
    line = subtitles.readline()
    if line == '':
      break
    line_number = int(line)
    time = subtitles.readline()
    subtitle = subtitles.readline()
    while True:
      line = subtitles.readline()
      if (line and not line == "\r\n"):
        subtitle += line
      else:
        break

    start, end = parse_timestamp(time)
    parse_silence(movie, line_number - 1, previous_end, start) 
    previous_end = end

    parse_subtitle(movie, line_number, start, end, subtitle)

  parse_silence(movie, line_number, previous_end)

def main():
  parser = argparse.ArgumentParser(description="prints ffmpeg commands to cut a video into clips from given subtitles.")
  parser.add_argument('movie', help="the file containing the movie")
  parser.add_argument('subtitles', help="the file containing the subtitles")

  args = parser.parse_args()
  subtitles = codecs.open(args.subtitles, "r", "utf-8-sig")

  parse_subtitles(args.movie, subtitles)
if __name__ == "__main__":
  main()
