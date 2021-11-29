mkdir -p ~/.streamlit/
sudo apt-get -y install apt-utils gcc libpq-dev libsndfile-dev
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
