class LoginHistoryController < ApplicationController
  def index
    user_id = Integer(params[:user_id])
    @logins = ActiveRecord::Base.connection.exec_query(
      "SELECT ip, at FROM logins WHERE user_id = #{user_id} ORDER BY at DESC"
    ).to_a
    render json: @logins
  end
end
