class GradeBookController < ApplicationController
  def index
    course = params[:course_id].to_i
    @grades = Grade.find_by_sql(
      ["SELECT student_id, grade FROM grades WHERE course_id = ?", course]
    )
    render :index
  end
end
