require "sinatra"
require "json"

DATA_DIR = "/srv/datasets".freeze

get "/datasets/preview" do
  dataset = params[:dataset]
  halt 400 unless dataset

  lines = IO.readlines(File.join(DATA_DIR, dataset)).first(20)
  content_type :json
  { dataset: dataset, head: lines.map(&:chomp) }.to_json
end
