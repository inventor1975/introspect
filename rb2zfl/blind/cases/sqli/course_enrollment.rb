class EnrollmentController < ApplicationController
  def index
    term = params[:term]
    ids = Enrollment.pluck(params[:group_col])
    @enrollments = Enrollment.where("term = '#{term}'").where(student_id: ids)
    render json: @enrollments
  end
end
