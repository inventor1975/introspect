def run
  c = "ls"
  c, n = params[:c], 1
  system(c)                           # REFUTED
end
