<?php

function get_username(int $a): string {
    return (string)$a;
}

$user = 5
     |> get_username(...)
     ?? 'default';

var_dump($user);
?>