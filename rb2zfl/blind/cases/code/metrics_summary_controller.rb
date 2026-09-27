class Stats
  def initialize(values) = @values = values
  def sum = @values.sum
  def mean = @values.empty? ? 0 : @values.sum.to_f / @values.size
  def median = @values.sort[@values.size / 2]
end

class MetricsSummaryController < ApplicationController
  ALLOWED = %w[sum mean median].freeze

  def show
    stats = Stats.new(Measurement.where(sensor_id: params[:sensor_id]).pluck(:value))
    op = ALLOWED.include?(params[:op]) ? params[:op] : "sum"
    render json: { op: op, value: stats.public_send(op) }
  end
end
