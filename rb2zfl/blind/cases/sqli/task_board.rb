class TaskBoardController < ApplicationController
  def index
    @tasks = Task.where(assignee_id: params[:assignee_id], status: params[:status])
                 .order(created_at: :desc)
    render json: @tasks
  end
end
