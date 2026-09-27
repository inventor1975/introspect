require "sinatra"

get "/doc" do
  a = params[:a].to_s
  halt 400 unless a =~ /\A[a-z0-9]+\z/
  File.read("docs/#{a}.md")
  b = params[:b].to_s
  halt 400 unless b.match?(/^[a-z]+$/) # ^ $ are LINE anchors: "x\n../../etc/passwd" passes
  File.read("docs/#{b}.md")
  c = params[:c].to_s
  halt 400 unless c =~ /\A[\w.\/-]+\z/ # anchored, but it allows ../
  File.read("docs/#{c}")
end
