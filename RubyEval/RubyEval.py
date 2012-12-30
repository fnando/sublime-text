import subprocess
import sublime, sublime_plugin

class EvalAsRuby:
    def ruby(self):
        try:
            return self.view.settings().get("ruby_eval").get("ruby")
        except AttributeError:
            return "ruby"

    def eval_as_ruby(self, script):
        proc = subprocess.Popen(self.ruby(),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE)

        ruby_input = u"""
            require 'stringio'

            io = StringIO.new
            begin
              $stdout = $stderr = io
              result = (lambda {
                %s
              }).call
            ensure
              $stdout = STDOUT
              $stderr = STDERR
            end

            if io.string.empty?
              case result
              when String
                print result
              else
                print result.inspect
              end
            else
              print io.string
            end
        """ % script

        output, error = proc.communicate(ruby_input.encode('utf-8'))
        output = output.strip()

        if proc.poll():
            output += "\n" + error

        return unicode(output ,encoding='utf-8')

class RubyEvalCommand(sublime_plugin.TextCommand, EvalAsRuby):
    def run(self, edit, output_to_editor=True):
        for region in self.view.sel():
            if region.a == region.b:
                # eval line
                region_of_line = self.view.line(region)
                script = self.view.substr(region_of_line)
                output = self.eval_as_ruby(script)
                if output_to_editor:
                    self.insert_output(output, region, edit, region_of_line.b, "\n")
                else:
                    pass # TODO
            else:
                # eval selected
                script = self.view.substr(region)
                output = self.eval_as_ruby(script)
                start = max(region.a, region.b)
                space = "" if script[-1] == "\n" else " "
                if output_to_editor:
                    self.insert_output(output, region, edit, start, space)
                else:
                    pass # TODO

    def insert_output(self, output, region, edit, start, space):
        self.view.insert(edit, start, space + output)
        self.view.sel().subtract(region)
        len_of_space = len(space)
        self.view.sel().add(
          sublime.Region(
            start + len_of_space,
            start + len_of_space + len(output.replace("\n", ''))))
