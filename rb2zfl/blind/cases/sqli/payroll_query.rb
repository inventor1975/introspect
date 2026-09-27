class PayrollController < ApplicationController
  def report
    year = params[:year]
    grade = params[:grade]
    sql = <<~SQL
      SELECT employee_id, gross, net
      FROM payroll
      WHERE fiscal_year = #{year} AND grade = '#{grade}'
    SQL
    @rows = ActiveRecord::Base.connection.select_all(sql).to_a
    render json: @rows
  end
end
