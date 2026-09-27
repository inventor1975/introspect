require "sinatra/base"

class ForumApp < Sinatra::Base
  get "/threads" do
    board = params[:board]
    threads = Thread2.where("board = ?", board).order(:bumped_at)
    threads.to_json
  end
end

class Thread2 < ActiveRecord::Base; end
