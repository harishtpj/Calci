PY="python"
SRC="calci.py"

task :default => [:run]

desc "Runs Calci Compiler"
task :run do
    puts "---> Running Compiler"
    sh "#{PY} #{SRC} #{ENV['ARGS']}",  verbose: false
end

desc "Cleans Working Directory by deleting files"
task :clean do
    rm_rf "calci\\__pycache__", verbose: false
    rm_rf "calci\\errors\\__pycache__", verbose: false
    rm_f Dir.glob("*.c"), verbose: false
    rm_f Dir.glob("*.exe"), verbose: false
    puts "---> Cleaned Directory by deleting files"
end