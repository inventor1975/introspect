class SessionActivityController < ApplicationController
  def index
    user_id = params[:user_id]
    conn = ActiveRecord::Base.connection
    @sessions = conn.execute(
      "SELECT * FROM sessions WHERE user_id = #{user_id} ORDER BY started_at DESC"
    )
    render :index
  end
end
