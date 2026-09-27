class DashboardLayout
  attr_reader :panels

  def initialize
    @panels = []
  end

  def panel(name, **opts)
    @panels << opts.merge(name: name)
  end
end

class DashboardLayoutsController < ApplicationController
  DASHBOARDS = {
    "sales" => "sales_overview",
    "ops" => "operations",
    "support" => "support_queue"
  }.freeze

  def show
    file = DASHBOARDS.fetch(params[:name], "sales_overview")
    path = Rails.root.join("config", "dashboards", "#{file}.rb")
    layout = DashboardLayout.new
    layout.instance_eval(File.read(path), path.to_s)
    render json: layout.panels
  end
end
