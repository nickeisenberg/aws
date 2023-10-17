source ~/.bashrc

export PATH="/usr/local/cuda/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"

function venv() { ?venv        [7/8]
    source /home/ubuntu/Software/venv/$1/bin/activate
}

