require "sinatra"

SCORE_EXPRESSION = ENV.fetch("SCORE_EXPRESSION", "likes * 2 + comments * 5")

get "/posts/:id/score" do
  likes = params[:likes].to_i
  comments = params[:comments].to_i
  "score=#{eval(SCORE_EXPRESSION)}"
end
