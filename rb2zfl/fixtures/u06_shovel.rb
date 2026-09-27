def run
  parts = ["ls"]
  parts << params[:c]
  system(parts.join(" "))             # REFUTED
end
