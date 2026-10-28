rule ssh_failures {
    source linux_auth;
    detect count(linux_auth.auth_failure) >= 5;
    in 60s;
    by src_ip;
    then alert "Repeated SSH login failures";
}
