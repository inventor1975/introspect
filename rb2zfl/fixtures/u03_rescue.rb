def run
  x = 1
rescue => e
  system(params[:c])                  # REFUTED (inside rescue)
end
