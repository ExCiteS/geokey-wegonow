"""Methods for converting data between systems or formats."""


def make_cm_url(url):
    """Turns a Geokey url into a Community Maps url."""
    protocol, address = url.split('//')
    address_parts = address.split('/')
    new_address_parts = []
    for i, part in enumerate(address_parts):
        if part == 'api':
            continue
        if i == 0 and '-gk-' in part:
            new_address_parts.append(part.replace('-gk-', '-cm-'))
        elif part.endswith('s'):
            new_address_parts.append(part[:-1])
        else:
            new_address_parts.append(part)
    return protocol + '//' + '/'.join(new_address_parts)
