# Normalises user supplied export names before they touch the disk.
module PathScrubber
  module_function

  def clean(name)
    name.to_s.strip.gsub("../", "").gsub("..\\", "")
  end
end
