from flask import Blueprint, request
from functools import wraps
from backend.app.utils.response import ok, bad_request, unauthorized
from backend.app.services.auth import verify_token
from backend.app.repositories import cities, air_quality, analytics
from datetime import datetime

bp = Blueprint('data', __name__, url_prefix='/data')

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return unauthorized('token_required')
        
        user_info = verify_token(token)
        if not user_info:
            return unauthorized('invalid_token')
        
        request.user = user_info
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/cities', methods=['GET'])
@require_login
def list_cities():
    try:
        q = request.args.get('q', default='', type=str)
        province = request.args.get('province', default=None, type=str)
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=20, type=int)
        
        page_size = min(page_size, 100)
        
        items, total, error = cities.get_all_cities(q, province, page, page_size)
        
        if error:
            return bad_request('query_failed')
        
        return ok('success', {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
        })
    except Exception as e:
        return bad_request('server_error')

@bp.route('/cities/<int:city_id>', methods=['GET'])
@require_login
def get_city(city_id):
    try:
        city = cities.get_city_by_id(city_id)
        if not city:
            return bad_request('city_not_found')
        
        return ok('success', city)
    except Exception as e:
        return bad_request('server_error')

@bp.route('/query', methods=['GET'])
@require_login
def query_air_quality():
    try:
        city_id = request.args.get('city_id', type=int)
        start_time = request.args.get('start_time', default=None, type=str)
        end_time = request.args.get('end_time', default=None, type=str)
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=20, type=int)

        if not city_id:
            return bad_request('city_id_required')
        
        if start_time:
            try:
                start_time = datetime.fromisoformat(start_time)
            except:
                return bad_request('invalid_start_time')
        
        if end_time:
            try:
                end_time = datetime.fromisoformat(end_time)
            except:
                return bad_request('invalid_end_time')
        
        page_size = min(page_size, 100)
        
        items, total, error = air_quality.query_air_quality_data(
            city_id, start_time, end_time, None, page, page_size
        )
        print(items, total, error)
        
        if error:
            return bad_request('query_failed')
        
        return ok('success', {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
        })
    except Exception as e:
        return bad_request('server_error')

@bp.route('/detail', methods=['GET'])
@require_login
def get_latest_detail():
    try:
        city_id = request.args.get('city_id', type=int)
        
        if not city_id:
            return bad_request('city_id_required')
        
        city = cities.get_city_by_id(city_id)
        if not city:
            return bad_request('city_not_found')
        
        data = air_quality.get_latest_air_quality(city_id)
        
        user_id = request.user.get('id')
        analytics.log_user_action(user_id, 'view_data', city_id)
        
        return ok('success', {
            'city': city,
            'latest_data': data,
        })
    except Exception as e:
        return bad_request('server_error')

@bp.route('/monthly-stats', methods=['GET'])
@require_login
def get_monthly_stats():
    try:
        city_id = request.args.get('city_id', type=int)
        months = request.args.get('months', default=12, type=int)
        
        if not city_id:
            return bad_request('city_id_required')
        
        city = cities.get_city_by_id(city_id)
        if not city:
            return bad_request('city_not_found')
        
        months = min(months, 24)
        items, error = air_quality.get_monthly_stats(city_id, months)
        
        if error:
            return bad_request('query_failed')
        
        return ok('success', {
            'city': city,
            'monthly_stats': items,
        })
    except Exception as e:
        return bad_request('server_error')
