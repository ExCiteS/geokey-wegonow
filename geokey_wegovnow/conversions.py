"""Methods for converting data between systems or formats."""


def make_cm_url(url):
    """Turns a Geokey url into a Community Maps url."""
    protocol, address = url.split('//')
    address_parts = address.split('/')
    new_address_parts = [address_parts[0]]
    for i, part in enumerate(address_parts[1:]):
        if part == 'api':
            continue
        if i == 1 and '-gk-' in part:
            new_part = part.replace('-gk-', '-cm-')
            new_address_parts.append(new_part)
        if part.endswith('s'):
            new_address_parts.append(part[:-1])
        else:
            new_address_parts.append(part)
    return protocol + '//' + '/'.join(new_address_parts)
