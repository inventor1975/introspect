class ActionsController < ApplicationController
  def run
    job = Job.find(1)
    job.public_send(params[:op])
    params[:type].constantize.new
    job.send("sort_by_#{params[:key]}") # a fixed prefix: only sort_by_* methods -> unknown, not proven
  end
end
