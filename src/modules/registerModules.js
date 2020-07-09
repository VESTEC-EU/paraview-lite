import DefaultComponent from 'paraview-lite/src/modules/Default';
import defaultModule from 'paraview-lite/src/modules/Default/module';

import CinemaReader from 'paraview-lite/src/modules/CinemaReader';
import cinemaReaderModule from 'paraview-lite/src/modules/CinemaReader/module';

import CinemaFiles from 'paraview-lite/src/modules/CinemaFiles';
import cinemaFilesModule from 'paraview-lite/src/modules/CinemaFiles/module';

export default function registerModules(store) {
  // --------------------------------------------------------------------------
  // Widget registering
  // --------------------------------------------------------------------------

  store.commit(
    'PVL_MODULES_ADD',
    Object.assign({}, cinemaFilesModule, { component: CinemaFiles })
  );

  store.commit(
    'PVL_MODULES_ADD',
    Object.assign({}, cinemaReaderModule, { component: CinemaReader })
  );

  // --------------------------------------------------------------------------
  // Proxy to UI mapping
  // --------------------------------------------------------------------------

  store.commit('PVL_PROXY_MODULE_BIND', {
    name: 'SphereSource',
    module: 'Sphere',
  });

  store.commit('PVL_PROXY_MODULE_BIND', {
    name: 'ConeSource',
    module: 'Cone',
  });

  store.commit('PVL_PROXY_MODULE_BIND', {
    name: 'Clip',
    module: 'Clip',
  });

  store.commit('PVL_PROXY_MODULE_BIND', {
    name: 'Cut',
    module: 'Slice',
  });
  store.commit('PVL_PROXY_MODULE_BIND', {
    name: 'Contour',
    module: 'Contour',
  });
  store.commit('PVL_PROXY_MODULE_BIND', {
    name: 'Threshold',
    module: 'Threshold',
  });
  store.commit('PVL_PROXY_MODULE_BIND', {
    name: 'StreamTracer',
    module: 'StreamTracer',
  });

  // --------------------------------------------------------------------------
  // Fallback mapping
  // --------------------------------------------------------------------------

  store.commit(
    'PVL_MODULES_ADD',
    Object.assign({}, defaultModule, {
      component: DefaultComponent,
      name: 'default',
    })
  );

  // --------------------------------------------------------------------------

  store.commit('PVL_PROXY_MODULE_BIND', {
    name: 'default',
    module: 'default',
  });
}
