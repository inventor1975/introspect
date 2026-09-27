def run
  c = params[:c]
  c += " -la"
  system(c)                           # REFUTED
end
