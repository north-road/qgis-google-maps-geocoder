# QGIS3 default
QGISDIR=.local/share/QGIS/QGIS3/profiles/default

PLUGIN_NAME = synthwave

EXTRAS = metadata.txt icon.png

EXTRA_DIRS =

default:

deploy:
	@echo
	@echo "------------------------------------------"
	@echo "Deploying (symlinking) plugin to your qgis3 directory."
	@echo "------------------------------------------"
	# The deploy  target only works on unix like operating system where
	# the Python plugin directory is located at:
	# $HOME/$(QGISDIR)/python/plugins
	ln -s `pwd`/$(PLUGIN_NAME) $(HOME)/$(QGISDIR)/python/plugins/${PWD##*/}

# The dclean target removes compiled python files from plugin directory
# also deletes any .git entry
dclean:
	@echo
	@echo "-----------------------------------"
	@echo "Removing any compiled python files."
	@echo "-----------------------------------"
	find $(PLUGIN_NAME) -iname "*.pyc" -delete
	find $(PLUGIN_NAME) -iname ".git" -prune -exec rm -Rf {} \;

zip: dclean
	@echo
	@echo "---------------------------"
	@echo "Creating plugin zip bundle."
	@echo "---------------------------"
	# The zip target deploys the plugin and creates a zip file with the deployed
	# content. You can then upload the zip file on http://plugins.qgis.org
	rm -f $(PLUGIN_NAME).zip
	zip -9r $(PLUGIN_NAME).zip $(PLUGIN_NAME) -x *.git* -x *__pycache__* -x *test*
