class StaffRosterController < ApplicationController
  def index
    dept = params[:department]
    @staff = Employee.where(department: dept).order(:last_name)
    render :index
  end
end
