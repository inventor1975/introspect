class ReportTemplate < ApplicationRecord
  TEMPLATE_DIR = Rails.root.join("app", "report_templates")

  validates :name, presence: true

  def self.body_for(name)
    File.read(TEMPLATE_DIR.join(name))
  end

  def render_with(values)
    ERB.new(self.class.body_for(name)).result_with_hash(values)
  end
end
