def run
  h = {}
  h[:c] = params[:c]
  system(h[:c])                       # REFUTED
end
