module StoragePaths
  class OutsideRoot < StandardError; end

  module_function

  def resolve!(root, relative)
    root = File.expand_path(root)
    candidate = File.expand_path(relative.to_s, root)
    unless candidate.start_with?(root + File::SEPARATOR)
      raise OutsideRoot, "refusing #{relative.inspect}"
    end
    candidate
  end
end
