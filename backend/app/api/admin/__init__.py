from flask import Blueprint, request
from functools import wraps
from backend.app.utils.response import ok, bad_request, unauthorized, forbidden
from backend.app.services.auth import verify_token
from backend.app.repositories import cities, sync_logs, analytics
from datetime import datetime, date, timedelta

bp = Blueprint('admin', __name__, url_prefix='/admin')

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return unauthorized('token_required')
        
        user_info = verify_token(token)
        if not user_info:
            return unauthorized('invalid_token')
        
        if user_info.get('role') != 'admin':
            return forbidden('admin_required')
        
        request.user = user_info
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/cities', methods=['POST'])
@require_admin
def create_city():
    try:
        data = request.get_json() or {}
        
        name = data.get('name', '').strip()
        province = data.get('province', '').strip() if data.get('province') else None
        lat = data.get('lat')
        lon = data.get('lon')
        
        if not name:
            return bad_request('name_required')
        
        city, error = cities.create_city(name, province, lat, lon)
        
        if error:
            return bad_request('create_failed')
        
        return ok(city, 'created')
    except Exception as e:
        return bad_request('server_error')

@bp.route('/cities/<int:city_id>', methods=['PUT'])
@require_admin
def update_city(city_id):
    try:
        city = cities.get_city_by_id(city_id)
        if not city:
            return bad_request('city_not_found')
        
        data = request.get_json() or {}
        
        updated_city, error = cities.update_city(
            city_id,
            name=data.get('name'),
            province=data.get('province'),
            lat=data.get('lat'),
            lon=data.get('lon')
        )
        
        if error:
            return bad_request('update_failed')
        
        return ok(updated_city, 'updated')
    except Exception as e:
        return bad_request('server_error')

@bp.route('/cities/<int:city_id>', methods=['DELETE'])
@require_admin
def delete_city(city_id):
    try:
        city = cities.get_city_by_id(city_id)
        if not city:
            return bad_request('city_not_found')
        
        success, error = cities.delete_city(city_id)
        
        if not success:
            return bad_request('delete_failed')
        
        return ok({}, 'deleted')
    except Exception as e:
        return bad_request('server_error')

@bp.route('/data/sync', methods=['POST'])
@require_admin
def trigger_sync():
    try:
        data = request.get_json() or {}
        source = data.get('source', 'AQICN').upper()
        
        if source not in ['AQICN', 'OPENAQ']:
            return bad_request('invalid_source')
        
        log_id, error = sync_logs.log_sync(
            sync_type='manual',
            data_source=source,
            start_time=datetime.utcnow(),
            status='in_progress'
        )
        
        if error:
            return bad_request('sync_failed')
        
        sync_logs.update_sync_log(
            log_id,
            end_time=datetime.utcnow(),
            status='success',
            success_count=0,
            fail_count=0,
            total_count=0
        )
        
        return ok({'sync_id': log_id}, 'sync_triggered')
    except Exception as e:
        return bad_request('server_error')

@bp.route('/data/sync-logs', methods=['GET'])
@require_admin
def get_sync_logs():
    try:
        start_date = request.args.get('start_date', default=None, type=str)
        end_date = request.args.get('end_date', default=None, type=str)
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=20, type=int)
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except:
                return bad_request('invalid_start_date')
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except:
                return bad_request('invalid_end_date')
        
        page_size = min(page_size, 100)
        
        items, total, error = sync_logs.get_sync_logs(start_date, end_date, page, page_size)
        
        if error:
            return bad_request('query_failed')
        
        return ok({
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
        }, 'success')
    except Exception as e:
        return bad_request('server_error')

@bp.route('/data/sync-stats', methods=['GET'])
@require_admin
def get_sync_stats():
    try:
        days = request.args.get('days', default=7, type=int)
        days = min(days, 90)
        
        stats, error = sync_logs.get_sync_stats(days)
        
        if error:
            return bad_request('query_failed')
        
        return ok(stats, 'success')
    except Exception as e:
        return bad_request('server_error')

@bp.route('/analytics/usage', methods=['GET'])
@require_admin
def get_usage_stats():
    try:
        days = request.args.get('days', default=7, type=int)
        days = min(days, 90)
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        dau_items, error1 = analytics.get_dau_stats(start_date, end_date)
        top_cities_items, error2 = analytics.get_top_cities(start_date, end_date, limit=5)
        feature_items, error3 = analytics.get_feature_usage(start_date, end_date)
        
        return ok({
            'dau': dau_items,
            'top_cities': top_cities_items,
            'feature_usage': feature_items,
        }, 'success')
    except Exception as e:
        return bad_request('server_error')
