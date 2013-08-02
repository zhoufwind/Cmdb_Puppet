class web{
    #package {'httpd':ensure=>present}
    package {'nginx':ensure=>present}
    #file {'/zhangshaozhi':
    #    ensure=>present,
    #    user=>'root',
    #    group=>'root',
    #    mode=>'0664',
    #}
    file {
        "/zhangshaozhi":
            ensure => present,
            owner => 'root',
            group => 'root',
            mode => '0644'
    }
}
