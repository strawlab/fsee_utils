
scripts = [
    # rfsee
    ('rfsee_server', 'rfsee.rfsee_server'),
    ('rfsee_demo_pipe', 'rfsee.demo.demo_pipe'),
    ('rfsee_demo_pipe_rotation', 'rfsee.demo.demo_pipe_rotation'),
    ('rfsee_demo_tcp', 'rfsee.demo.demo_tcp'),
    ('rfsee_demo_tcp_benchmark', 'rfsee.demo.demo_tcp_benchmark'),
]


# this is the format for setuptools
console_scripts = map(lambda s: '%s = %s:main' % (s[0], s[1]), scripts)
