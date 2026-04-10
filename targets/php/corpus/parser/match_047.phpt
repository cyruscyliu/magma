<?php

echo match (match ('b') { default => 'b' }) {
    'a' => 100,
    'b' => 200,
    'c' => 300
};

?>