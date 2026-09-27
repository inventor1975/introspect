class EmployeeDirectoryController < ApplicationController
  def index
    dept = params[:department]
    @employees = Employee.select("id, name, title")
                         .where("department = '#{dept}'")
                         .order(params[:order_by])
    render :index
  end
end
