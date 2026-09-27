require "sinatra"

class Bucket
  def initialize(root, name)
    @root = root
    @name = name
  end

  def path_for(key)
    File.join(@root, @name, key)
  end

  def read(key)
    File.binread(path_for(key))
  end
end

BUCKET_ROOT = "/srv/object-store".freeze

get "/objects" do
  bucket = Bucket.new(BUCKET_ROOT, params[:bucket].to_s)
  content_type "application/octet-stream"
  bucket.read(params[:key].to_s)
end
