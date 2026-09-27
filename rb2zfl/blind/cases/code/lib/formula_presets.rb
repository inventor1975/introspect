# Fixed set of reporting formulas. Keys are exposed to clients, bodies are not.
module FormulaPresets
  FORMULAS = {
    "margin"   => "(revenue - cost) / revenue.to_f",
    "markup"   => "(revenue - cost) / cost.to_f",
    "per_unit" => "revenue / [units, 1].max.to_f"
  }.freeze

  def self.lookup(name)
    FORMULAS.fetch(name) { FORMULAS["margin"] }
  end
end
