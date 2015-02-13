{% from "salt/package-map.jinja" import pkgs with context %}

include:
  - salt.pkgrepo

{% if pillar['salt']['minion']['roles'] is defined %}
/etc/salt/grains:
  file.managed:
    - makedirs: true
    - template: jinja
    - source: salt://salt/templates/grains
{% endif %}

salt-minion:
  pkg.installed:
    - name: {{ pkgs['salt-minion'] }}
  file.managed:
    - name: /etc/salt/minion
    - template: jinja
    - source: salt://salt/templates/minion
  service.running:
    - enable: true
    - restart: true
    - watch:
      - pkg: salt-minion
      - file: salt-minion
      {% if pillar['salt']['minion']['roles'] is defined %}
      - file: /etc/salt/grains
      {% endif %}

