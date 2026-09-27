class Leaderboard
  def initialize(entries)
    @entries = entries
  end

  def sort_by_score
    @entries.sort_by { |e| -e.score }
  end

  def sort_by_name
    @entries.sort_by(&:name)
  end

  def sort_by_recent
    @entries.sort_by { |e| -e.updated_at.to_i }
  end
end

class LeaderboardsController < ApplicationController
  def show
    board = Leaderboard.new(Entry.where(season: params[:season]).to_a)
    sorter = "sort_by_#{params[:sort]}"
    sorter = "sort_by_score" unless board.respond_to?(sorter)
    render json: board.public_send(sorter)
  end
end
