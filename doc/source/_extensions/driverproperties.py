# From https://www.sphinx-doc.org/en/master/development/tutorials/todo.html

import docutils.statemachine
import sphinx.locale

sphinx.locale.admonitionlabels['shortname'] = ''
sphinx.locale.admonitionlabels['built_in_by_default'] = ''  # 'Built-in by default'
sphinx.locale.admonitionlabels['supports_create'] = ''  # 'Create() 지원'
sphinx.locale.admonitionlabels['supports_createcopy'] = ''  # 'CreateCopy() 지원'
sphinx.locale.admonitionlabels['supports_georeferencing'] = ''  # '지리참조 작업 지원'
sphinx.locale.admonitionlabels['supports_virtualio'] = ''  # 'VirtualIO 지원'
sphinx.locale.admonitionlabels['supports_multidimensional'] = ''  # 'Supports multidimensional'
sphinx.locale.admonitionlabels['deprecated_driver'] = ''  # 'Driver is deprecated and marked for removal'

def setup(app):
    app.add_node(shortname,
                 html=(visit_shortname_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('shortname', ShortName)

    app.add_node(built_in_by_default,
                 html=(visit_built_in_by_default_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('built_in_by_default', BuiltInByDefault)

    app.add_node(build_dependencies,
                 html=(visit_build_dependencies_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('build_dependencies', BuildDependencies)

    app.add_node(supports_create,
                 html=(visit_supports_create_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('supports_create', CreateDirective)

    app.add_node(supports_createcopy,
                 html=(visit_supports_createcopy_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('supports_createcopy', CreateCopyDirective)

    app.add_node(supports_georeferencing,
                 html=(visit_supports_georeferencing_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('supports_georeferencing', GeoreferencingDirective)

    app.add_node(supports_virtualio,
                 html=(visit_supports_virtualio_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('supports_virtualio', VirtualIODirective)

    app.add_node(supports_multidimensional,
                 html=(visit_supports_multidimensional_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('supports_multidimensional', MultiDimensionalDirective)

    app.add_node(deprecated_driver,
                 html=(visit_deprecated_driver_node, depart_node),
                 latex=(visit_admonition, depart_node),
                 text=(visit_admonition, depart_node))
    app.add_directive('deprecated_driver', DeprecatedDriverDirective)

    app.connect('env-purge-doc', purge_driverproperties)

    return { 'parallel_read_safe': True, 'parallel_write_safe': True }

from docutils import nodes

def visit_admonition(self, node):
    self.visit_admonition(node)

def depart_node(self, node):
    self.depart_admonition(node)

class shortname(nodes.Admonition, nodes.Element):
    pass

def visit_shortname_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('admonition shortname')))

class built_in_by_default(nodes.Admonition, nodes.Element):
    pass

def visit_built_in_by_default_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('admonition built_in_by_default')))

class build_dependencies(nodes.Admonition, nodes.Element):
    pass

def visit_build_dependencies_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('admonition build_dependencies')))

class supports_create(nodes.Admonition, nodes.Element):
    pass

def visit_supports_create_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('admonition supports_create')))

class supports_createcopy(nodes.Admonition, nodes.Element):
    pass

def visit_supports_createcopy_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('admonition supports_createcopy')))

class supports_georeferencing(nodes.Admonition, nodes.Element):
    pass

def visit_supports_georeferencing_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('admonition supports_georeferencing')))

class supports_virtualio(nodes.Admonition, nodes.Element):
    pass

def visit_supports_virtualio_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('admonition supports_virtualio')))

class supports_multidimensional(nodes.Admonition, nodes.Element):
    pass

def visit_supports_multidimensional_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('admonition supports_multidimensional')))

class deprecated_driver(nodes.Admonition, nodes.Element):
    pass

def visit_deprecated_driver_node(self, node):
    self.body.append(self.starttag(
            node, 'div', CLASS=('danger deprecated_driver')))

from docutils.parsers.rst import Directive


from sphinx.locale import _


def finish_directive(_self, directive, node):

    env = _self.state.document.settings.env

    targetid = "%s-%d" % (directive, env.new_serialno(directive))
    targetnode = nodes.target('', '', ids=[targetid])

    _self.state.nested_parse(_self.content, _self.content_offset, node)

    if not hasattr(env, 'all_' + directive):
        setattr(env, 'all_' + directive, [])
    getattr(env, 'all_' + directive).append({
        'docname': env.docname,
        'lineno': _self.lineno,
        directive: node.deepcopy(),
        'target': targetnode,
    })

    return [targetnode, node]


class ShortName(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        node = shortname('\n'.join(self.content))
        node += nodes.title(_('드라이버 단축 이름'), _('드라이버 단축 이름'))

        return finish_directive(self, 'shortname', node)


class BuiltInByDefault(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        if not self.content:
            self.content = docutils.statemachine.StringList(['이 드라이버는 기본적으로 내장되어 있습니다.'])
        node = built_in_by_default('\n'.join(self.content))
        node += nodes.title(_('기본 내장 드라이버'), _('기본 내장 드라이버'))

        return finish_directive(self, 'built_in_by_default', node)


class BuildDependencies(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        assert self.content, "build_dependencies 지시문에 내용을 정의해야 합니다."
        node = build_dependencies('\n'.join(self.content))
        node += nodes.title(_('빌드 의존성'), _('빌드 의존성'))

        return finish_directive(self, 'build_dependencies', node)


class CreateDirective(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        if not self.content:
            self.content = docutils.statemachine.StringList(['이 드라이버는 :cpp:func:`GDALDriver::Create` 작업을 지원합니다.'])
        node = supports_create('\n'.join(self.content))
        node += nodes.title(_('Create() 지원'), _('Create() 지원'))

        return finish_directive(self, 'supports_create', node)

class CreateCopyDirective(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        if not self.content:
            self.content = docutils.statemachine.StringList(['이 드라이버는 :cpp:func:`GDALDriver::CreateCopy` 작업을 지원합니다.'])
        node = supports_createcopy('\n'.join(self.content))
        node += nodes.title(_('CreateCopy() 지원'), _('CreateCopy() 지원'))

        return finish_directive(self, 'supports_createcopy', node)


class GeoreferencingDirective(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        if not self.content:
            self.content = docutils.statemachine.StringList(['이 드라이버는 지리참조 작업을 지원합니다.'])
        node = supports_georeferencing('\n'.join(self.content))
        node += nodes.title(_('지리참조 작업 지원'), _('지리참조 작업 지원'))

        return finish_directive(self, 'supports_georeferencing', node)


class VirtualIODirective(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        if not self.content:
            self.content = docutils.statemachine.StringList(['이 드라이버는 :ref:`virtual I/O operations (/vsimem/, etc.) <virtual_file_systems>` 를 지원합니다.'])
        node = supports_virtualio('\n'.join(self.content))
        node += nodes.title(_('VirtualIO 지원'), _('VirtualIO 지원'))

        return finish_directive(self, 'supports_virtualio', node)


class MultiDimensionalDirective(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        if not self.content:
            self.content = docutils.statemachine.StringList(['이 드라이버는 :ref:`multidim_raster_data_model` 을 지원합니다.'])
        node = supports_virtualio('\n'.join(self.content))
        node += nodes.title(_('다중차원 API 지원'), _('다중차원 API 지원'))

        return finish_directive(self, 'supports_multidimensional', node)


class DeprecatedDriverDirective(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):

        explanation = []
        version_targeted_for_removal = [c[len('version_targeted_for_removal:'):].strip() for c in self.content if
                                        c.startswith('version_targeted_for_removal:')]
        if version_targeted_for_removal:
            explanation.append(
                "GDAL {}에서 이 드라이버를 제거할지 고려 중입니다.".format(version_targeted_for_removal[0]))
        else:
            explanation.append("이후 GDAL 배포판에서 이 드라이버를 제거할지 고려 중입니다.")

        message = [c[len('message:'):].strip() for c in self.content if
                                        c.startswith('message:')]
        if message:
            explanation.append(message[0])
        else:
            explanation.append("해당 포맷의 모든 데이터셋을 더 자주 사용되는 다른 포맷으로 변환할 것을 추천합니다.")

        explanation.append("이후 GDAL 버전에서 이 드라이버가 필요한 경우, 이 드라이버가 얼마나 중요한지 설명하려면"
                           "(먼저 기존 티켓을 찾아본 다음) https://github.com/OSGeo/gdal 에서 티켓을 생성하십시오."
                           "(그래도 GDAL 프로젝트가 해당 드라이버를 제거할 수도 있습니다.)")

        env_variable = [c[len('env_variable:'):].strip() for c in self.content if
                        c.startswith('env_variable:')]
        if env_variable:
            explanation.append("퇴출된 드라이버 사용을 활성화하려면 {} 환경설정 옵션 /"
                               " 환경 변수를 YES로 설정해야만 합니다.".format(env_variable[0]))

        self.content = docutils.statemachine.StringList(explanation)

        node = deprecated_driver('\n'.join(self.content))
        node += nodes.title(_('Deprecated'), _('Deprecated'))

        return finish_directive(self, 'deprecated_driver', node)


def purge_driverproperties(app, env, docname):
    for directive in ['all_shortname',
                      'all_built_in_by_default',
                      'all_build_dependencies',
                      'all_supports_create',
                      'all_supports_createcopy',
                      'all_supports_georeferencing',
                      'all_supports_virtualio',
                      'all_supports_multidimensional',
                      'all_deprecated_driver']:
        if hasattr(env, directive):
            setattr(env, directive, [ embed for embed in getattr(env, directive) if embed['docname'] != docname])
