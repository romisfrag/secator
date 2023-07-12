from secator.decorators import task
from secator.definitions import (DEFAULT_DNS_WORDLIST, DOMAIN, HOST, RATE_LIMIT, RETRIES, THREADS, WORDLIST)
from secator.output_types import Subdomain
from secator.tasks._categories import ReconDns

@task()
class dnsxbrute(ReconDns):
    """dnsx is a fast and multi-purpose DNS toolkit designed for running various probes through the retryabledns library."""
    cmd = 'dnsx'
    json_flag = '-json'
    input_flag = '-domain'
    file_flag = '-domain'
    opt_key_map = {
        RATE_LIMIT: 'rate-limit',
        RETRIES: 'retry',
        THREADS: 'threads',
    }
    opts = {
        WORDLIST: {'type': str, 'short': 'w','default': DEFAULT_DNS_WORDLIST, 'help': 'Wordlist'},
    }
    output_map = {
        Subdomain: {
            HOST: 'host',
            DOMAIN: lambda x: ".".join(x['host'].split('.')[1:])
        }
    }
    install_cmd = 'go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest'